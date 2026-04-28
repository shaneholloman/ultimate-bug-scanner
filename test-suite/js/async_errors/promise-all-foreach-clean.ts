type User = {
  id: string;
  displayName: string;
};

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${encodeURIComponent(id)}`);
  return response.json() as Promise<User>;
}

export async function warmUserCache(ids: string[]): Promise<User[]> {
  const tasks = ids.map((id) => fetchUser(id));
  const users: User[] = [];
  for (const task of tasks) {
    users.push(await task);
  }
  return users;
}
