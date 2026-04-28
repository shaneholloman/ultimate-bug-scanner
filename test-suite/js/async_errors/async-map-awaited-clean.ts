type User = { id: string; email: string };

async function sendWelcomeEmail(user: User): Promise<void> {
  const response = await fetch(`/api/welcome/${user.id}`, {
    method: "POST",
    body: JSON.stringify({ email: user.email }),
  });
  if (!response.ok) {
    throw new Error("welcome email failed");
  }
}

export async function inviteUsers(users: User[]): Promise<void> {
  try {
    const tasks = users.map(async (user) => {
      await sendWelcomeEmail(user);
    });
    for (const task of tasks) {
      await task;
    }
  } catch (error) {
    throw new Error(`failed to invite users: ${String(error)}`);
  }
}
