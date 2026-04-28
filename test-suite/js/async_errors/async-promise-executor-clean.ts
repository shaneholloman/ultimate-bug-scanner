export function loadProfile(cache: Map<string, string>, userId: string): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    const cachedProfile = cache.get(userId);
    if (cachedProfile === undefined) {
      reject(new Error("profile missing"));
      return;
    }
    resolve(cachedProfile);
  });
}
