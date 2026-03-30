# Publishing Guide

This repo is prepared to publish as:

```bash
@lizmotia/ag-kit
```

After publish, the intended install flow is:

```bash
npx @lizmotia/ag-kit init
```

Or:

```bash
npm install -g @lizmotia/ag-kit
ag-kit init
```

## Before You Publish

1. Make sure your npm account can publish under the `@lizmotia` scope.
2. If your npm username or org scope is different, update the `name` field in [package.json](./package.json) first.
3. Run:

```bash
npm login
npm run pack:check
```

## Publish

```bash
npm publish
```

This package already includes:

- `publishConfig.access = public`
- the `ag-kit` binary
- the `ag-codex` compatibility alias

## Verify

After publish, verify with:

```bash
npm view @lizmotia/ag-kit version
npx @lizmotia/ag-kit init
```
