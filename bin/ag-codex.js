#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const packageRoot = path.resolve(__dirname, "..");
const sourceAgentsDir = path.join(packageRoot, ".agents");

function printHelp() {
  console.log(`Antigravity Codex Bridge CLI

Usage:
  ag-codex init [--path <project-dir>] [--force] [--dry-run]
  ag-codex update [--path <project-dir>] [--dry-run]
  ag-codex status [--path <project-dir>]
  ag-codex help

Examples:
  npx antigravity-codex-bridge init
  npx antigravity-codex-bridge init --path ./my-app
  npm install -g antigravity-codex-bridge
  ag-codex init
`);
}

function parseArgs(argv) {
  const args = {
    command: argv[2] ?? "help",
    path: process.cwd(),
    force: false,
    dryRun: false
  };

  for (let i = 3; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--force") {
      args.force = true;
      continue;
    }

    if (arg === "--dry-run") {
      args.dryRun = true;
      continue;
    }

    if (arg === "--path") {
      const next = argv[i + 1];
      if (!next) {
        throw new Error("Missing value for --path");
      }
      args.path = path.resolve(next);
      i += 1;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  return args;
}

function shouldSkip(relPath) {
  const normalized = relPath.split(path.sep).join("/");
  const basename = path.basename(relPath);

  return (
    normalized === "plugins" ||
    normalized.startsWith("plugins/") ||
    basename === "__pycache__" ||
    basename === "preview.pid" ||
    basename === "preview.log"
  );
}

function copyDir(sourceDir, targetDir) {
  fs.mkdirSync(targetDir, { recursive: true });

  for (const entry of fs.readdirSync(sourceDir, { withFileTypes: true })) {
    const sourcePath = path.join(sourceDir, entry.name);
    const relPath = path.relative(sourceAgentsDir, sourcePath);

    if (shouldSkip(relPath)) {
      continue;
    }

    const targetPath = path.join(targetDir, entry.name);

    if (entry.isDirectory()) {
      copyDir(sourcePath, targetPath);
      continue;
    }

    fs.copyFileSync(sourcePath, targetPath);
  }
}

function countItems(dir, predicate) {
  if (!fs.existsSync(dir)) {
    return 0;
  }

  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter(predicate)
    .length;
}

function initProject(targetRoot, { force, dryRun }) {
  const targetAgentsDir = path.join(targetRoot, ".agents");

  if (!fs.existsSync(sourceAgentsDir)) {
    throw new Error(`Source .agents directory not found at ${sourceAgentsDir}`);
  }

  if (!fs.existsSync(targetRoot)) {
    throw new Error(`Target path does not exist: ${targetRoot}`);
  }

  if (fs.existsSync(targetAgentsDir) && !force) {
    throw new Error(
      `Target already contains .agents at ${targetAgentsDir}. Use --force to overwrite.`
    );
  }

  if (dryRun) {
    console.log(`[dry-run] Would install .agents into: ${targetAgentsDir}`);
    return;
  }

  fs.rmSync(targetAgentsDir, { recursive: true, force: true });
  copyDir(sourceAgentsDir, targetAgentsDir);

  console.log("Installed Antigravity Codex Bridge");
  console.log(`Target: ${targetAgentsDir}`);
  console.log("Next steps:");
  console.log("1. Open the project in VS Code");
  console.log("2. Go to the CODEX tab");
  console.log("3. Reload the window or force reload skills");
  console.log("4. Use skills like $brainstorm, $create, $debug");
}

function statusProject(targetRoot) {
  const targetAgentsDir = path.join(targetRoot, ".agents");

  if (!fs.existsSync(targetAgentsDir)) {
    console.log(`No .agents installation found in: ${targetRoot}`);
    process.exitCode = 1;
    return;
  }

  const counts = {
    agents: countItems(path.join(targetAgentsDir, "agents"), (entry) => entry.isFile()),
    skills: countItems(path.join(targetAgentsDir, "skills"), (entry) => entry.isDirectory()),
    workflows: countItems(path.join(targetAgentsDir, "workflows"), (entry) => entry.isFile()),
    scripts: countItems(path.join(targetAgentsDir, "scripts"), (entry) => entry.isFile())
  };

  console.log("Antigravity Codex Bridge status");
  console.log(`Path: ${targetAgentsDir}`);
  console.log(`Agents: ${counts.agents}`);
  console.log(`Skills: ${counts.skills}`);
  console.log(`Workflows: ${counts.workflows}`);
  console.log(`Scripts: ${counts.scripts}`);
}

function main() {
  try {
    const args = parseArgs(process.argv);

    switch (args.command) {
      case "init":
        initProject(args.path, args);
        break;
      case "update":
        initProject(args.path, { ...args, force: true });
        break;
      case "status":
        statusProject(args.path);
        break;
      case "help":
      case "--help":
      case "-h":
        printHelp();
        break;
      default:
        throw new Error(`Unknown command: ${args.command}`);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    console.error("Run `ag-codex help` for usage.");
    process.exit(1);
  }
}

main();
