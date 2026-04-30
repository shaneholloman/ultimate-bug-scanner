import jwt from "jsonwebtoken";
import { decode as decodeToken, verify } from "jsonwebtoken";
import { decodeJwt } from "jose";
import jwtDecode from "jwt-decode";

type Request = {
  headers: {
    authorization?: string;
  };
};

const SECRET = process.env.JWT_TEST_SECRET ?? "local-test-secret";

export function trustsDecodedRole(req: Request): string | undefined {
  const token = req.headers.authorization?.replace("Bearer ", "") ?? "";
  const claims = jwt.decode(token) as { role?: string } | null;
  return claims?.role;
}

export function trustsAliasedDecode(token: string): unknown {
  return decodeToken(token);
}

export function trustsJoseDecode(token: string): unknown {
  return decodeJwt(token);
}

export function trustsJwtDecodePackage(token: string): unknown {
  return jwtDecode(token);
}

export function verifiesButIgnoresExpiration(token: string): unknown {
  return verify(token, SECRET, { algorithms: ["HS256"], ignoreExpiration: true });
}

export function acceptsNoneAlgorithm(token: string): unknown {
  return jwt.verify(token, SECRET, { algorithms: ["none"] });
}
