import java.util.concurrent.CompletableFuture;

public class AsyncErrors {
    public static String loadUser() {
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "user");
        try {
            return future.get();
        } catch (Exception ex) {
            throw new IllegalStateException("failed", ex);
        }
    }

    public static void logChain() {
        CompletableFuture.supplyAsync(() -> "value")
            .thenApply(String::toUpperCase)
            .exceptionally(ex -> {
                System.err.println("chain failed " + ex.getMessage());
                return "fallback";
            })
            .thenAccept(System.out::println);
    }

    public static void main(String[] args) {
        loadUser();
        logChain();
    }
}
