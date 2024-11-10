#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#define MAX_REQUEST_SIZE 1024

// Vulnerable function that doesn't properly check buffer boundaries
void process_request(int client_sock) {
    char buffer[MAX_REQUEST_SIZE];
    int bytes_received;

    // Receive the HTTP request
    bytes_received = recv(client_sock, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received <= 0) {
        perror("recv failed");
        close(client_sock);
        return;
    }

    // Null-terminate the string
    buffer[bytes_received] = '\0';

    // Vulnerable response processing: buffer overflow vulnerability here
    // This is a buffer overflow vulnerability.  If the request contains
    // more than MAX_REQUEST_SIZE bytes, it will overflow the buffer.
    printf("Request received: %s\n", buffer);

    // If the request contains "GET /evil" in it, it causes a stack overflow
    if (strstr(buffer, "GET /evil") != NULL) {
        printf("Triggering buffer overflow...\n");
        char evil_data[1000];
        memset(evil_data, 'A', sizeof(evil_data));  // This will overflow the stack
        evil_data[999] = '\0';
    }

    // Send a simple HTTP response
    char *response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!";
    send(client_sock, response, strlen(response), 0);

    // Close the connection
    close(client_sock);
}

// Simple vulnerable HTTP server
void start_server(int port) {
    int server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);

    // Create the socket
    server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock == -1) {
        perror("Socket creation failed");
        exit(1);
    }

    // Set up the server address structure
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    // Bind the socket to the address and port
    if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Bind failed");
        close(server_sock);
        exit(1);
    }

    // Start listening for incoming connections
    if (listen(server_sock, 10) == -1) {
        perror("Listen failed");
        close(server_sock);
        exit(1);
    }

    printf("Server started on port %d\n", port);

    // Main loop to accept incoming client connections
    while (1) {
        client_sock = accept(server_sock, (struct sockaddr *)&client_addr, &client_addr_len);
        if (client_sock == -1) {
            perror("Accept failed");
            continue;
        }

        // Process the request
        process_request(client_sock);
    }
}

int main() {
    // Start the vulnerable HTTP server on port 8080
    start_server(8080);
    return 0;
}