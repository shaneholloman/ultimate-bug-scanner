import https from "https";
import axios from "axios";
import tls from "tls";

export const unsafeAgent = new https.Agent({
  rejectUnauthorized: false,
});

export const client = axios.create({
  httpsAgent: new https.Agent({
    rejectUnauthorized: false,
  }),
});

export function connectToInternalService(host: string): tls.TLSSocket {
  return tls.connect({
    host,
    port: 443,
    rejectUnauthorized: false,
  });
}

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

export const testEnv = {
  NODE_TLS_REJECT_UNAUTHORIZED: "0",
};
