export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Send POST to trigger update', { status: 405 });
    }

    const url = `https://api.github.com/repos/${env.REPO_OWNER}/${env.REPO_NAME}/actions/workflows/${env.WORKFLOW_ID}/dispatches`;
    const body = JSON.stringify({ ref: 'main' });

    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Cloudflare Worker'
      },
      body: body
    });

    if (resp.ok) {
      return new Response(JSON.stringify({ ok: true, message: 'Workflow started' }), {
        headers: { 'Content-Type': 'application/json' }
      });
    } else {
      return new Response(JSON.stringify({ ok: false, message: 'GitHub error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};