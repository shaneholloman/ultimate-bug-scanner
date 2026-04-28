export function loadProfile(userId: string): Promise<string> {
  return new Promise<string>(async (resolve) => {
    const response = await fetch(`/api/profiles/${userId}`);
    if (!response.ok) {
      throw new Error("profile load failed");
    }
    resolve(await response.text());
  });
}
