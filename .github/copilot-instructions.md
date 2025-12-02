# Copilot Instructions for Vercel HTML Starter

## Architecture Overview
This is a static HTML website deployed on Vercel with Edge Middleware for server-side logic. Key components:
- `index.html`: Main page with content, Vercel Analytics script, and external CSS
- `middleware.js`: Applies security headers globally using `@vercel/edge`
- `vercel.json`: Configures build to skip compilation, serve from root directory

Data flows: Static content served directly; middleware intercepts requests for headers.

## Developer Workflows
- **Local Development**: Run `vercel dev` to simulate Vercel environment with middleware
- **Deployment**: Push to `main` branch for auto-deploy, or use `vercel --prod` for manual
- **Authentication**: Run `vercel login` before CLI commands
- **No Build Required**: Static files served as-is; no compilation step

## Key Patterns
- **Middleware Usage**: Import `next` from `@vercel/edge` to pass requests with custom headers (see `middleware.js`)
- **Analytics Integration**: Include `<script defer src="/_vercel/insights/script.js"></script>` for Vercel Analytics
- **Security Headers**: Use middleware for global headers like HSTS, CSP equivalents
- **Vercel Config**: Set `framework: null`, `buildCommand: null` in `vercel.json` for static sites

## Examples
- Adding headers: `return next({ headers: { 'X-Custom': 'value' } })`
- External styles: Link to CDN like `https://cdn.jsdelivr.net/npm/@exampledev/new.css`
- Deployment check: Verify middleware headers in browser dev tools after deploy

## Integration Points
- Vercel Edge Network: Middleware runs at edge for low-latency headers
- GitHub: Auto-deploys on push to main
- External: CDN for styles, Vercel Analytics for tracking</content>
<parameter name="filePath">/workspaces/hack/.github/copilot-instructions.md