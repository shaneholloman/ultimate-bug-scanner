package main

import (
    "fmt"
    "net/http"
)

func fireAndForget(urls []string) {
    for _, url := range urls {
        go func(u string) {
            resp, err := http.Get(u)
            resp.Body.Close()
            fmt.Println("status", resp.Status, err)
        }(url)
    }
}

func main() {
    fireAndForget([]string{"https://example.com"})
}
