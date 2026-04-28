async function submitProfile(): Promise<void> {
  await Promise.resolve();
}

export function ProfileButton() {
  return (
    <button
      onClick={async () => {
        await submitProfile();
      }}
    >
      Save
    </button>
  );
}
