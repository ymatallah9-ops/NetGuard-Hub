#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/time.h>

// دالة ذكية تجلب البوابة الافتراضية للشبكة (المحاكية لأمر ip route)
int get_default_gateway(char* gateway_buf) {
    FILE *f = fopen("/proc/net/route", "r");
    if (!f) return 0;

    char line[100], iface[20];
    unsigned long dest, gw;
    
    while (fgets(line, sizeof(line), f)) {
        if (sscanf(line, "%s %lx %lx", iface, &dest, &gw) == 3) {
            if (dest == 0) { // Dest = 00000000 تعني المسار الافتراضي (Default Route)
                struct in_addr addr;
                addr.s_addr = gw;
                strcpy(gateway_buf, inet_ntoa(addr));
                fclose(f);
                return 1;
            }
        }
    }
    fclose(f);
    return 0;
}

// دالة فحص المنفذ العادية والسريعة (TCP Connect)
int check_port_status(const char* ip, int port) {
    int sock;
    struct sockaddr_in server;
    
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) return 0;
    
    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 400000; 
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv));

    server.sin_addr.s_addr = inet_addr(ip);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);

    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        close(sock);
        return 0;
    }
    close(sock);
    return 1;
}

// دالة التحقق من نشاط الجهاز
int is_device_alive(const char* ip) {
    if (check_port_status(ip, 80) || check_port_status(ip, 443) || check_port_status(ip, 22)) {
        return 1;
    }
    return 0;
}
