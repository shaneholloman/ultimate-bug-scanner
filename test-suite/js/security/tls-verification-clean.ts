import https from "https";
import axios from "axios";
import tls from "tls";

const privateCa = "-----BEGIN CERTIFICATE-----\\n...\\n-----END CERTIFICATE-----";

export const safeAgent = new https.Agent({
  ca: privateCa,
  rejectUnauthorized: true,
});

export const client = axios.create({
  httpsAgent: safeAgent,
});

export function connectToInternalService(host: string): tls.TLSSocket {
  return tls.connect({
    host,
    port: 443,
    ca: privateCa,
    rejectUnauthorized: true,
  });
}

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "1";

export const testEnv = {
  NODE_TLS_REJECT_UNAUTHORIZED: "1",
};
