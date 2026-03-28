export default {
  async fetch(request, env, ctx) {
    const upstream = env.UPSTREAM_ORIGIN || "https://verses1.onrender.com";
    const incomingUrl = new URL(request.url);
    const target = new URL(upstream);

    incomingUrl.hostname = target.hostname;
    incomingUrl.protocol = target.protocol;
    incomingUrl.port = target.port || "";

    const init = {
      method: request.method,
      headers: new Headers(request.headers),
      redirect: "follow",
    };

    if (request.method !== "GET" && request.method !== "HEAD") {
      init.body = request.body;
    }

    return fetch(incomingUrl.toString(), init);
  },
};
