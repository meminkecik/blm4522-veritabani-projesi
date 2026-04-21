def run_explain_analyze(conn, query):
    try:
        cur = conn.cursor()
        explain_query = f"EXPLAIN (ANALYZE, FORMAT JSON) {query}"
        cur.execute(explain_query)

        result = cur.fetchone()[0][0]

        execution_time = result['Execution Time']
        plan = result['Plan']
        scan_type = plan['Node Type']

        print(f"Tarama Türü    : {scan_type}")
        print(f"Çalışma Süresi : {execution_time} ms")

        cur.close()
        return execution_time
    except Exception as e:
        print(f"Analiz sırasında hata oluştu: {e}")
        return None