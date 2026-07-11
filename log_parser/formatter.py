import json
from statistics import Statistics


def print_report(aggregator: Statistics, malformed_lines: int) -> None:

    total = aggregator.total_requests
    total_errors = aggregator.total_errors
    total_pass = aggregator.total_pass
    ip_counts = aggregator.ip_counts

    if total == 0:
        print("\nNo data was processed. Check your log file.")
        return

    print("\n" + "=" * 55)
    print("FINAL INFRASTRUCTURE ANALYSIS REPORT")
    print("=" * 55)
    print(f"Total Requests Processed : {total:,}")
    print(f"Malformed Lines          : {malformed_lines:,}")
    print(f"Unique Client IPs        : {len(ip_counts):,}")
    print(f"Total Error Count        : {sum(total_errors.values()):,}")
    print(f"Overall Error Rate       : {sum(total_errors.values()) / total * 100:.2f}%")
    print("-" * 55)

    print(" TOP 10 ENDPOINTS")
    print(f" {'Endpoint':<40} | {'Requests':<10}")
    print(" " + "-" * 52)
    for endpoint, count in aggregator.get_top_endpoints(limit=10):
        print(f"  {endpoint:<39} | {count:<10,}")
    print("-" * 55)

    print(" TOP 10 CLIENT IPS")
    print(f" {'IP Address':<40} | {'Requests':<10}")
    print(" " + "-" * 52)
    for ip, count in aggregator.get_top_ips(limit=10):
        print(f"  {ip:<39} | {count:<10,}")
    print("-" * 55)

    print("24-HOUR TRAFFIC DISTRIBUTION (HISTOGRAM)")
    print(" " + "-" * 55)
    try:
        hourly_data = aggregator.get_hourly_report()
        max_traffic_in_an_hour = max(hourly_data.values())
    except ValueError:
        return

    max_bar_length = 30
    all_hours = [
        "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
        "20", "21", "22", "23",
    ]

    for hour in all_hours:
        count = hourly_data.get(hour)
        if count:
            bar_length = int((count / max_traffic_in_an_hour) * max_bar_length)
        else:
            continue

        bar = "█" * bar_length
        peak_tag = " [PEAK]" if count == max_traffic_in_an_hour and count > 0 else ""
        print(f"  {int(hour):02d}:00 | {bar:<30} | {count:<8,}{peak_tag}")

    print("=" * 55 + "\n")


def export_json(aggregator: Statistics, malformed_lines: int) -> str:
    total = aggregator.total_requests
    total_errors = sum(aggregator.total_errors.values())
    error_rate = total_errors / total * 100 if total else 0.0

    data = {
        "total_requests": total,
        "malformed_lines": malformed_lines,
        "unique_ips": len(aggregator.ip_counts),
        "total_errors": total_errors,
        "error_rate": round(error_rate, 2),
        "top_endpoints": [
            {"endpoint": ep, "count": c}
            for ep, c in aggregator.get_top_endpoints(10)
        ],
        "top_ips": [
            {"ip": ip, "count": c}
            for ip, c in aggregator.get_top_ips(10)
        ],
        "hourly_traffic": {
            hour: aggregator.hourly_traffic.get(hour, 0)
            for hour in [f"{h:02d}" for h in range(24)]
        },
    }
    return json.dumps(data, indent=2)
