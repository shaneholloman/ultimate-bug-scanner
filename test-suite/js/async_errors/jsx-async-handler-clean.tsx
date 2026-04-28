async function submitProfile(): Promise<void> {
  return Promise.resolve();
}

function reportError(error: unknown): void {
  console.error(error);
}

export function ProfileButton() {
  return (
    <button
      onClick={() => {
        void submitProfile().catch(reportError);
      }}
    >
      Save
    </button>
  );
}
