export default function UserNotRegisteredError() {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-background p-6 text-center text-foreground">
      <div className="max-w-md space-y-2">
        <h1 className="text-xl font-semibold">Access unavailable</h1>
        <p className="text-sm text-muted-foreground">
          This account is not registered for the application.
        </p>
      </div>
    </div>
  );
}
