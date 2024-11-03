name = ['db_h_srv_h', 'db_n_srv_n', 'db_d_srv_d', 'db_r_srv_r', 'db_h_srv_n', 'db_h_srv_d', 'db_h_srv_r', 'db_n_srv_h', 'db_d_srv_h', 'db_r_srv_h']

configs = 10

with open('compose.yaml', 'a') as file:
    file.write("version: '3.1'\n")
    file.write("services:\n")

    for i in range(configs):
        file.write(f'  zabbix-server-{name[i]}:\n')
        file.write('    image: zabbix/zabbix-server-pgsql:latest\n')
        file.write(f'    container_name: zabbix_server_{name[i]}\n')
        file.write('    restart: unless-stopped\n')
        file.write('    networks:\n')
        file.write(f'      - zabbix_{name[i]}\n')
        file.write('    volumes:\n')
        if name[i][-1] == 'h':
            file.write(f'      - /zabbix_data/{name[i]}/server:/var/lib/zabbix\n')
        elif name[i][-1] == 'n':
            file.write(f'      - /zabbix_data/noname/{name[i]}/server:/var/lib/zabbix\n')
        elif name[i][-1] == 'd':
            file.write(f'      - /zabbix_data/dexp/{name[i]}/server:/var/lib/zabbix\n')
        elif name[i][-1] == 'r':
            file.write(f'      - /zabbix_data/radeon/{name[i]}/server:/var/lib/zabbix\n')
        file.write('    environment:\n')
        file.write(f'      DB_SERVER_HOST: zabbix-postgres-{name[i]}\n      POSTGRES_USER: zabbix\n      POSTGRES_PASSWORD: zabbix_pass\n      ZBX_JAVAGATEWAY: zabbix-java-gateway-{name[i]}\n')
        file.write('    depends_on:\n')
        file.write(f'      - zabbix-postgres-{name[i]}\n\n')

        file.write(f'  zabbix-postgres-{name[i]}:\n')
        file.write('    image: postgres:13\n')
        file.write(f'    container_name: zabbix_database_{name[i]}\n')
        file.write('    restart: unless-stopped\n')
        file.write('    networks:\n')
        file.write(f'      - zabbix_{name[i]}\n')
        file.write('    volumes:\n')
        if name[i][3] == 'h':
            file.write(f'      - /zabbix_data/{name[i]}/db:/var/lib/postgresql/data\n')
        elif name[i][3] == 'n':
            file.write(f'      - /zabbix_data/noname/{name[i]}/db:/var/lib/postgresql/data\n')
        elif name[i][3] == 'd':
            file.write(f'      - /zabbix_data/dexp/{name[i]}/db:/var/lib/postgresql/data\n')
        elif name[i][3] == 'r':
            file.write(f'      - /zabbix_data/radeon/{name[i]}/db:/var/lib/postgresql/data\n')
        file.write('    environment:\n')
        file.write('      POSTGRES_USER: zabbix\n      POSTGRES_PASSWORD: zabbix_pass\n      POSTGRES_DB: zabbix\n')
        
        file.write(f'  zabbix-web-{name[i]}:\n')
        file.write('    image: zabbix/zabbix-web-nginx-pgsql:latest\n')
        file.write(f'    container_name: zabbix_web_{name[i]}\n')
        file.write('    restart: unless-stopped\n')
        file.write('    networks:\n')
        file.write(f'      - zabbix_{name[i]}\n')
        file.write('    ports:\n')
        port = 8080 + i
        file.write(f'      - {port}:8080\n')
        file.write('    environment:\n')
        file.write(f'      DB_SERVER_HOST: zabbix-postgres-{name[i]}\n      POSTGRES_USER: zabbix\n      POSTGRES_PASSWORD: zabbix_pass\n      ZBX_SERVER_NAME: Zabbix Server {name[i]}\n')
        file.write('    depends_on:\n')
        file.write(f'      - zabbix-server-{name[i]}\n\n')
        
        file.write(f'  zabbix-java-gateway-{name[i]}:\n')
        file.write('    image: zabbix/zabbix-java-gateway:latest\n')
        file.write(f'    container_name: zabbix_java_{name[i]}\n')
        file.write('    restart: unless-stopped\n')
        file.write('    networks:\n')
        file.write(f'      - zabbix_{name[i]}\n\n')

    file.write('networks:\n')

    for i in range(configs):
        file.write(f'  zabbix_{name[i]}:\n')
        file.write('    driver: bridge\n')
