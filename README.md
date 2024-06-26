[中文](https://github.com/wlhtea/Suno2openai/blob/main/README_ZH.md) English

# Suno2openai

> Integrated based on [SunoSongsCreator](https://github.com/yihong0618/SunoSongsCreator)
> and [Suno-API](https://github.com/SunoAI-API/Suno-API) projects, offering standardized service interfaces compliant
> with
> OpenAI formats.

## Changelog

- 2024.6.05 Separate database names from user names
- 2024.6.03 Added suno-v3.5 model call and cdn link fetch.
- 2024.4.14 Support for non-streaming output with `stream=False` docker version 0.1.1 No need to update if you don't
  need this feature.
- 2024.4.14 Updated a script to automatically retrieve cookies from registered Outlook emails and write them into the
  database.
- 2024.4.12 **Completed integration of new-api and one-api**, select OpenAI calls, and input the project deployment
  address (no need for /v1/); the key can be left empty.
- 2024.4.10 Due to Suno's official updates, some project features were inoperable, now modified. Please re-pull the
  projects pulled before 2024/4/10 15:04; Docker to be updated later (already updated, be mindful of the version number
  when pulling).

## ✨ Project Highlights

- **OpenAI Format Calls**: Supports streaming output.
- **Front-end Compatibility**: Compatible with front-end projects like `chat-next-web`.
- **Docker Deployment**: Simplifies deployment process, supports `docker-compose`, `docker`.
- **Multiple Cookie Management**: Implements rotation of multiple cookies.

## 🚀 Future Plans

- Introduce request queueing optimizations.
- Support for custom parameters (such as `tags`, `prompt`, `style`, and song continuation).
- Explore development of official-like frontend pages.
- Welcome valuable suggestions! 📧 **Email**: 1544007699@qq.com

---

## 🫙 Docker Deployment

This tutorial provides step-by-step guidance on running a Docker container with specific environment variables and port
mappings. For the purpose of this guide, sensitive information such as SQL names, passwords, and IP addresses will be
replaced with placeholders.

## Prerequisites

- Docker is installed on your machine.
- Basic knowledge of Docker CLI.

## Steps

1. **Pull Docker Image**

   Ensure the Docker image `wlhtea/suno2openai:latest` is available on your machine. If not, you can pull it from the
   Docker repository using:

   ```bash
   docker pull wlhtea/suno2openai:latest
   ```

2. **Run Docker Container**

   Run the Docker container using necessary environment variables and port mappings.
   Replace `<SQL_NAME>`, `<SQL_PASSWORD>`, and `<SQL_IP>` with your actual SQL database connection values. These should
   be kept confidential and not shared publicly.

   ```bash
      docker run -d --name wsunoapi \
      -p 8000:8000 \
      -e USER_NAME='<USER_NAME>'
      -e SQL_NAME='<SQL_NAME>' \
      -e SQL_PASSWORD='<SQL_PASSWORD>' \
      -e SQL_IP='<SQL_IP>' \
      -e SQL_DK=3306 \
      --restart=always \
      wlhtea/suno2openai:latest
   ```

   ### **example**
   ```         
   docker run -d --name wsunoapi \
         -p 8000:8000 \
         -e USER_NAME=suno2openaiUsername
         -e SQL_NAME=suno2openaiSQLname \
         -e SQL_PASSWORD=12345678 \
         -e SQL_IP=100.101.102.103 \
         -e SQL_DK=3306 \
         --restart=always \
         wlhtea/suno2openai:latest
   ```

**Parameter Explanation:**

- `-d`: Run the container in detached mode and logger.info the container ID.
- `--name wsunoapi`: Name your container `wsunoapi` for easy reference.
- `-p 8000:8000`: Map the container's 8000 port to the host machine's 8000 port.
- `-e`: Set environment variables for your container.
- `--restart=always`: Ensure the container always restarts, unless manually stopped.

**Add Cookie to Database**
Simply open the database and add cookies with the remaining count (an automatic import feature will be added later).

   ```mysql
      id = int
      cookie = Cookie
      count = int
      working = 0
   ```

Database may report error: 'NoneType' object has no attribute '
items', [check here if correct](https://github.com/wlhtea/Suno2openai/issues/10)

5. **Access the Application**

   Once the container is running, the application inside should be accessible via `http://localhost:8000` or the 8000
   port of your Docker host machine's IP address.

## Note

Before running the Docker container, make sure you replace placeholders like `<SQL_NAME>`, `<SQL_PASSWORD>`, `<SQL_IP>`,
and `<your-session-id>` with actual values.

## 📦 Docker-Compose Deployment

_Update Time: 2024/4/7 18:18_

### Clone the Project to Your Server

```bash
git clone https://github.com/wlhtea/Suno2openai.git
```

### Create a Database

Create a database (name it as you wish), remember to save the password, and ensure the database permissions are set
correctly (allow connections from all IPs or only from Docker container IPs).

### Configure Environment Variables

**Rename the `env.example` file to `.env` and fill in the corresponding details:**

```plaintext
SQL_NAME=<Database Name>
SQL_PASSWORD=<Database Password>
SQL_IP=<Database Host IP>
SQL_DK=3306 # Database port
USER_NAME=<Database Username>
```

### Enter the Project Directory

```bash
cd Suno2openai
```

### Update Cookie

### Start Docker

```bash
docker compose build && docker compose up
```

**Notes**:

- **Security Group Configuration**: Ensure the port 8000 is open.
- **HTTPS Support**: If the frontend project uses HTTPS, the proxy URL of this project should also use HTTPS.

## 🍪 Obtaining Cookies

### For Personal Use

Edit the `update_cookie_to_sql.py` file and insert your cookies into the array below:

```python
cookies = ['cookie1', 'cookie2']
```

![cookie位置示例](https://cdn.linux.do/uploads/default/original/3X/5/1/518adc3a227e60dc759a69da2335778e9dcd3854.png)

## 🔌 Integrating new-api(one-api)

In the channel's proxy settings, enter the project address as `http://<server IP>:8000`. HTTPS and a domain name are
recommended.

## 🎉 Effect Display

![效果图](https://github.com/wlhtea/Suno2openai/assets/115779315/3bcf2cee-770f-46a9-8438-b8bbfced0143)

## 💌 Internship Opportunities

If interested in welcoming a third-year student with experience in data analysis and front-end/back-end development for
an internship, please contact:

- 📧 **Email**: 1544007699@qq.com

**Support Us**: If you find this project helpful, please do not hesitate to star it ⭐! We welcome any form of support
and suggestions, let’s progress together!
