#include <stdio.h>
#include <stdint.h>
#include <stddef.h> // لتعريف size_t بشكل قياسي

struct ipv4_header {
    uint8_t  version_ihl;
    uint8_t  tos;
    uint16_t total_length;
    uint16_t id;
    uint16_t flags_offset;
    uint8_t  ttl;
    uint8_t  protocol;
    uint16_t checksum;
    uint32_t src_ip;
    uint32_t dest_ip;
};

int32_t parse_ipv4_packet(const uint8_t* buffer, size_t len, uint8_t* proto_out) {
    // 1. التحقق من أن المؤشرات ليست فارغة لضمان استقرار الأداة
    if (buffer == NULL || proto_out == NULL) return -2; 
    
    // 2. التحقق من الحجم الأدنى لتروّيسة IPv4 كما أضفت أنت
    if (len < 20) return -1; 
    
    // 3. فك الترويسة واستخراج البروتوكول
    const struct ipv4_header* ip = (const struct ipv4_header*)buffer;
    *proto_out = ip->protocol;
    
    return 0; // نجاح العملية
}
