#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const BASE_DIR = "/home/arhiv/maceret-case-evidence";

console.log(
  "🕵️ PORTAL AUDIT AGENT - Finding Broken Links & Missing Functions\n",
);
console.log("=".repeat(70));

const issues = {
  missingFunctions: [],
  missingFiles: [],
  brokenLinks: [],
  orphanedButtons: [],
};

function scanHTMLForFunctions(html) {
  const functionCalls = [];
  const definedFunctions = [];

  const onclickMatches = html.match(/onclick="([^"]+)"/g) || [];
  onclickMatches.forEach((match) => {
    const func = match.match(/onclick="([^"]+)"/)[1].replace("()", "");
    functionCalls.push(func);
  });

  const definedFuncMatches = html.match(/function\s+(\w+)/g) || [];
  definedFuncMatches.forEach((match) => {
    const func = match.replace("function ", "");
    definedFunctions.push(func);
  });

  return { functionCalls, definedFunctions };
}

function scanForFileReferences(html) {
  const refs = [];

  const hrefMatches =
    html.match(/href="([^"]+\.(pdf|md|json|yaml|html))"/g) || [];
  hrefMatches.forEach((match) => {
    const file = match.match(/href="([^"]+)"/)[1];
    refs.push({ type: "href", file });
  });

  const srcMatches = html.match(/src="([^"]+\.(js|css|png|jpg|svg))"/g) || [];
  srcMatches.forEach((match) => {
    const file = match.match(/src="([^"]+)"/)[1];
    refs.push({ type: "src", file });
  });

  const onclickMatches = html.match(/onclick="([^(]+\([^)]*\))"/g) || [];
  onclickMatches.forEach((match) => {
    const call = match.match(/onclick="([^"]+)"/)[1];
    if (call.includes("loadPdfByCodeDirect") || call.includes("viewFile")) {
      const fileMatch = call.match(/'([^']+)'/);
      if (fileMatch) {
        refs.push({ type: "onclick", file: fileMatch[1] });
      }
    }
  });

  return refs;
}

function checkFilesExist(refs) {
  refs.forEach((ref) => {
    let fullPath = path.join(BASE_DIR, ref.file);
    if (ref.file.startsWith("Downloads/")) {
      fullPath = path.join(BASE_DIR, ref.file);
    } else if (!ref.file.startsWith("http")) {
      fullPath = path.join(BASE_DIR, "Downloads", ref.file);
    }

    if (!fs.existsSync(fullPath)) {
      issues.missingFiles.push({
        file: ref.file,
        type: ref.type,
        fullPath,
      });
    }
  });
}

function scanJSONYAMLFiles() {
  const jsonYamlFiles = [
    "Downloads/registry.json",
    "Downloads/history.json",
    "Downloads/integrity-registry.json",
    "Downloads/corpus_documents.yaml",
    "Downloads/evidence_project/registry/api_nodes.json",
    "Downloads/evidence_project/registry/file_registry.json",
  ];

  jsonYamlFiles.forEach((relativePath) => {
    const fullPath = path.join(BASE_DIR, relativePath);
    if (!fs.existsSync(fullPath)) return;

    try {
      const content = fs.readFileSync(fullPath, "utf8");
      const data = relativePath.endsWith(".yaml")
        ? content
        : JSON.parse(content);

      if (data.files || data.documents || data.evidence) {
        const files = data.files || data.documents || data.evidence || [];
        files.forEach((item) => {
          const filename = item.file || item.path || item.name || item;
          if (
            filename &&
            typeof filename === "string" &&
            !filename.startsWith("http") &&
            !filename.includes("://")
          ) {
            let fullFilePath = path.join(BASE_DIR, "Downloads", filename);
            if (!fs.existsSync(fullFilePath)) {
              issues.missingFiles.push({
                file: filename,
                type: "registry reference",
                source: relativePath,
              });
            }
          }
        });
      }
    } catch (e) {
      console.log(`⚠️  Error parsing ${relativePath}: ${e.message}`);
    }
  });
}

function analyzeButtonsVsFunctions(html) {
  const buttonPatterns = [
    /<button[^>]*>([^<]*)<\/button>/gi,
    /<a[^>]*class="[^"]*btn[^"]*"[^>]*>([^<]*)<\/a>/gi,
    /<div[^>]*class="[^"]*btn[^"]*"[^>]*>/gi,
  ];

  let buttons = [];
  buttonPatterns.forEach((pattern) => {
    const matches = html.match(pattern) || [];
    buttons = [...buttons, ...matches];
  });

  buttons.forEach((btn) => {
    const hasOnclick = btn.includes("onclick=");
    const hasHref = btn.includes("href=");
    const text = btn.replace(/<[^>]+>/g, "").trim();

    if (
      !hasOnclick &&
      !hasHref &&
      text.length > 0 &&
      !text.includes("▼") &&
      !text.includes("▶")
    ) {
      issues.orphanedButtons.push({
        text: text.substring(0, 50),
        html: btn.substring(0, 100),
      });
    }
  });
}

async function main() {
  console.log("\n📂 Loading index.html...");
  const htmlPath = path.join(BASE_DIR, "index.html");
  const html = fs.readFileSync(htmlPath, "utf8");

  console.log("🔍 Scanning for function calls vs definitions...");
  const { functionCalls, definedFunctions } = scanHTMLForFunctions(html);

  const uniqueCalls = [...new Set(functionCalls)];
  uniqueCalls.forEach((func) => {
    if (!definedFunctions.includes(func) && !func.includes("(")) {
      issues.missingFunctions.push(func);
    }
  });

  console.log("🔗 Scanning file references...");
  const fileRefs = scanForFileReferences(html);
  checkFilesExist(fileRefs);

  console.log("📊 Analyzing JSON/YAML registries...");
  scanJSONYAMLFiles();

  console.log("🎯 Finding orphaned buttons...");
  analyzeButtonsVsFunctions(html);

  console.log("\n" + "=".repeat(70));
  console.log("📋 AUDIT RESULTS\n");

  if (issues.missingFunctions.length > 0) {
    console.log(
      "❌ MISSING FUNCTIONS (" + issues.missingFunctions.length + "):",
    );
    issues.missingFunctions.forEach((f) => console.log("   - " + f));
  } else {
    console.log("✅ All function calls resolved");
  }

  if (issues.missingFiles.length > 0) {
    console.log("\n❌ MISSING FILES (" + issues.missingFiles.length + "):");
    const uniqueMissing = [...new Set(issues.missingFiles.map((f) => f.file))];
    uniqueMissing.slice(0, 30).forEach((f) => console.log("   - " + f));
    if (uniqueMissing.length > 30) {
      console.log("   ... and " + (uniqueMissing.length - 30) + " more");
    }
  } else {
    console.log("\n✅ All referenced files exist");
  }

  if (issues.orphanedButtons.length > 0) {
    console.log("\n⚠️  ORPHANED BUTTONS (no onclick/href):");
    issues.orphanedButtons.slice(0, 10).forEach((b) => {
      console.log('   - "' + b.text + '"');
    });
  }

  const totalIssues =
    issues.missingFunctions.length +
    issues.missingFiles.length +
    issues.orphanedButtons.length;
  console.log("\n" + "=".repeat(70));
  console.log("📊 TOTAL ISSUES FOUND: " + totalIssues);
  console.log("=".repeat(70));

  fs.writeFileSync(
    path.join(BASE_DIR, "portal-audit-report.json"),
    JSON.stringify(issues, null, 2),
  );
  console.log("\n💾 Full report saved to: portal-audit-report.json");
}

main();
