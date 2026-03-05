#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const BASE_DIR = "/home/arhiv/maceret-case-evidence";
const LOG_FILE = "/home/arhiv/maceret-case-evidence/audit-log.json";
const STATE_FILE = "/home/arhiv/maceret-case-evidence/audit-state.json";

let auditLog = [];
let lastAuditState = {};

function loadState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      lastAuditState = JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
    }
  } catch (e) {
    lastAuditState = {};
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function log(message, type = "INFO") {
  const entry = {
    timestamp: new Date().toISOString(),
    type,
    message,
  };
  auditLog.push(entry);
  console.log(`[${type}] ${message}`);
}

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
    if (!file.startsWith("http")) {
      refs.push({ type: "href", file });
    }
  });

  return refs;
}

function checkFilesExist(refs) {
  const missing = [];
  refs.forEach((ref) => {
    let fullPath = path.join(BASE_DIR, ref.file);
    if (!fs.existsSync(fullPath)) {
      missing.push(ref.file);
    }
  });
  return missing;
}

function analyzeButtonsVsFunctions(html) {
  const buttonMatches = html.match(/<button[^>]*>([^<]*)<\/button>/gi) || [];
  const orphaned = [];

  buttonMatches.forEach((btn) => {
    const hasOnclick = btn.includes("onclick=");
    const hasForm = btn.includes('type="submit"');
    const text = btn.replace(/<[^>]+>/g, "").trim();

    if (!hasOnclick && !hasForm && text.length > 0) {
      orphaned.push(text);
    }
  });
  return orphaned;
}

function getRegistryStats() {
  const stats = { total: 0, void: 0, verified: 0 };

  try {
    const registryPath = path.join(BASE_DIR, "Downloads/registry.json");
    if (fs.existsSync(registryPath)) {
      const data = JSON.parse(fs.readFileSync(registryPath, "utf8"));
      if (data.evidence_triggers && Array.isArray(data.evidence_triggers)) {
        stats.total = data.evidence_triggers.length;
      }
      if (data.fraudData && Array.isArray(data.fraudData)) {
        stats.void = data.fraudData.length;
      }
      stats.verified = stats.total - stats.void;
    }

    const fraudPath = path.join(BASE_DIR, "index.html");
    const html = fs.readFileSync(fraudPath, "utf8");
    const fraudMatch = html.match(/const fraudData = \[([\s\S]*?)\];/);
    if (fraudMatch) {
      const fraudItems = fraudMatch[1].match(/\{[^}]+code:/g);
      if (fraudItems) {
        stats.void = fraudItems.length;
        stats.verified = stats.total - stats.void;
      }
    }
  } catch (e) {
    log(`Registry parse error: ${e.message}`, "WARN");
  }

  return stats;
}

function compareWithPrevious(currentIssues, previousIssues) {
  const changes = {
    newIssues: [],
    resolvedIssues: [],
    unchanged: [],
  };

  const prevFiles = new Set(previousIssues.missingFiles || []);
  const currFiles = new Set(currentIssues.missingFiles || []);

  currentIssues.missingFiles.forEach((f) => {
    if (!prevFiles.has(f)) {
      changes.newIssues.push({ type: "missingFile", file: f });
    }
  });

  (previousIssues.missingFiles || []).forEach((f) => {
    if (!currFiles.has(f)) {
      changes.resolvedIssues.push({ type: "resolvedFile", file: f });
    }
  });

  return changes;
}

function runAudit() {
  console.log("\n" + "=".repeat(70));
  console.log("🕵️ PORTAL AUTO-AUDIT AGENT v2.0");
  console.log("⏰ " + new Date().toLocaleString());
  console.log("=".repeat(70));

  loadState();

  const issues = {
    missingFunctions: [],
    missingFiles: [],
    orphanedButtons: [],
    timestamp: new Date().toISOString(),
  };

  log("Loading index.html...");
  const htmlPath = path.join(BASE_DIR, "index.html");
  const html = fs.readFileSync(htmlPath, "utf8");

  log("Scanning functions...");
  const { functionCalls, definedFunctions } = scanHTMLForFunctions(html);

  const uniqueCalls = [...new Set(functionCalls)];
  uniqueCalls.forEach((func) => {
    if (!definedFunctions.includes(func) && !func.includes("(")) {
      issues.missingFunctions.push(func);
    }
  });

  log("Scanning file references...");
  const fileRefs = scanForFileReferences(html);
  issues.missingFiles = checkFilesExist(fileRefs);

  log("Analyzing buttons...");
  issues.orphanedButtons = analyzeButtonsVsFunctions(html);

  log("Getting registry stats...");
  const stats = getRegistryStats();

  const currentState = {
    missingFiles: issues.missingFiles,
    orphanedButtons: issues.orphanedButtons,
    stats,
    timestamp: issues.timestamp,
  };

  const changes = compareWithPrevious(currentState, lastAuditState);

  console.log("\n" + "-".repeat(70));
  console.log("📊 AUDIT RESULTS");
  console.log("-".repeat(70));

  console.log(`\n📁 Files: ${issues.missingFiles.length} missing`);
  console.log(`🎯 Buttons: ${issues.orphanedButtons.length} orphaned`);
  console.log(
    `📋 Registry: ${stats.total} total, ${stats.void} void, ${stats.verified} verified`,
  );

  if (changes.newIssues.length > 0) {
    console.log("\n🆕 NEW ISSUES:");
    changes.newIssues.forEach((i) => console.log(`   + ${i.file}`));
  }

  if (changes.resolvedIssues.length > 0) {
    console.log("\n✅ RESOLVED:");
    changes.resolvedIssues.forEach((i) => console.log(`   - ${i.file}`));
  }

  if (changes.newIssues.length === 0 && changes.resolvedIssues.length === 0) {
    console.log("\n⚖️ No changes since last audit");
  }

  saveState(currentState);

  const report = {
    timestamp: issues.timestamp,
    stats,
    issues: {
      missingFilesCount: issues.missingFiles.length,
      orphanedButtonsCount: issues.orphanedButtons.length,
    },
    changes,
  };

  const logPath = path.join(BASE_DIR, "audit-history.json");
  let history = [];
  try {
    if (fs.existsSync(logPath)) {
      history = JSON.parse(fs.readFileSync(logPath, "utf8"));
    }
  } catch (e) {}

  history.push(report);
  if (history.length > 100) history = history.slice(-100);

  fs.writeFileSync(logPath, JSON.stringify(history, null, 2));

  console.log("\n" + "=".repeat(70));
  console.log("✅ Audit complete");
  console.log("=".repeat(70));

  return report;
}

function scheduleLoop(intervalMs = 3600000) {
  console.log(
    `\n🔄 Auto-audit enabled. Running every ${intervalMs / 1000 / 60} minutes.`,
  );
  console.log("Press Ctrl+C to stop.\n");

  runAudit();

  setInterval(() => {
    try {
      runAudit();
    } catch (e) {
      log(`Audit error: ${e.message}`, "ERROR");
    }
  }, intervalMs);
}

const args = process.argv.slice(2);

if (args.includes("--once")) {
  runAudit();
} else if (args.includes("--daemon")) {
  const interval = parseInt(args[args.indexOf("--daemon") + 1]) || 3600000;
  scheduleLoop(interval);
} else {
  console.log("Usage:");
  console.log("  node auto-audit-agent.js --once      - Run audit once");
  console.log(
    "  node auto-audit-agent.js --daemon     - Run as daemon (hourly)",
  );
  console.log(
    "  node auto-audit-agent.js --daemon 300000 - Run every 5 minutes",
  );
}
