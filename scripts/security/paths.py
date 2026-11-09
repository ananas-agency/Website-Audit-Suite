"""The exposed-files probe's address lists. Data only.

Each entry is (path, kind). Kinds: "secret" (can hold passwords, keys, code or data), "info" (only helps an
attacker map the site), "admin" (a management tool that should not be open to everyone) and "backdoor" (a
name commonly used by hacking tools). Only status, content type and length are ever recorded.
"""
from __future__ import annotations


def _build(**kinds):
    return tuple((p, kind) for kind, paths in kinds.items() for p in paths)


CORE_PATHS = _build(
    secret=(
        "/.git/HEAD", "/.git/config", "/.git-credentials", "/.svn/entries", "/.hg/hgrc",
        "/.env", "/.env.local", "/.env.production", "/.env.development", "/.env.backup", "/.env.save",
        "/.htpasswd", "/.htaccess", "/web.config",
        "/.aws/credentials", "/.ssh/id_rsa", "/id_rsa", "/.bash_history",
        "/sftp-config.json", "/.vscode/sftp.json", "/.ftpconfig",
        "/docker-compose.yml", "/docker-compose.override.yml",
        "/backup.zip", "/backup.tar.gz", "/backup.sql", "/backup.sql.gz", "/database.sql",
        "/database.sql.gz", "/db.sql", "/db.sql.gz", "/dump.sql", "/site.zip", "/site.tar.gz", "/www.zip",
        "/error_log", "/error.log", "/debug.log", "/logs/error.log",
        "/server-status", "/server-info",
    ),
    info=("/.DS_Store", "/Thumbs.db", "/.idea/workspace.xml", "/swagger-ui.html", "/swagger.json",
          "/openapi.json", "/api-docs"),
)

PLATFORM_PATHS = {
    "php": _build(
        secret=("/phpinfo.php", "/info.php", "/i.php", "/test.php", "/php.php", "/pi.php", "/phpversion.php",
                "/php_info.php", "/php_errorlog", "/.user.ini", "/config.php.bak", "/config.php.old",
                "/install.php", "/setup.php", "/installer.php", "/installer-backup.php"),
        info=("/composer.json", "/composer.lock", "/vendor/composer/installed.json"),
        admin=("/adminer.php", "/adminer/", "/phpmyadmin/", "/pma/"),
        backdoor=("/shell.php", "/cmd.php", "/wso.php", "/c99.php", "/r57.php", "/alfa.php"),
    ),
    "wordpress": _build(
        secret=("/wp-config.php.bak", "/wp-config.php.old", "/wp-config.php.save", "/wp-config.php~",
                "/.wp-config.php.swp", "/wp-content/debug.log"),
        info=("/wp-json/wp/v2/users", "/readme.html"),
    ),
    "laravel": _build(secret=("/storage/logs/laravel.log", "/_ignition/health-check"),
                      admin=("/telescope", "/horizon")),
    "symfony": _build(secret=("/_profiler", "/app_dev.php")),
    "drupal": _build(
        secret=("/sites/default/settings.php.bak", "/sites/default/settings.php.old",
                "/sites/default/settings.php~"),
        info=("/CHANGELOG.txt", "/core/CHANGELOG.txt"),
    ),
    "joomla": _build(
        secret=("/configuration.php.bak", "/configuration.php.old", "/configuration.php~"),
        info=("/administrator/manifests/files/joomla.xml",),
    ),
    "magento": _build(
        secret=("/app/etc/env.php.bak", "/app/etc/local.xml", "/var/log/system.log", "/var/log/exception.log"),
        admin=("/downloader/",),
    ),
    "craft": _build(secret=("/storage/logs/web.log",)),
    "node": _build(
        secret=("/.npmrc", "/npm-debug.log", "/yarn-error.log", "/ecosystem.config.js"),
        info=("/package.json", "/package-lock.json", "/yarn.lock"),
    ),
    "python": _build(
        secret=("/settings.py", "/local_settings.py", "/config.py", "/db.sqlite3", "/__debug__/"),
        info=("/requirements.txt", "/Pipfile.lock"),
    ),
    "rails": _build(
        secret=("/config/database.yml", "/config/secrets.yml", "/config/master.key", "/log/development.log",
                "/log/production.log", "/rails/info/properties", "/rails/info/routes"),
        info=("/Gemfile", "/Gemfile.lock"),
    ),
    "java": _build(
        secret=("/actuator/env", "/actuator/heapdump", "/actuator/configprops", "/jolokia", "/WEB-INF/web.xml"),
        info=("/actuator",),
        admin=("/manager/html", "/jmx-console"),
        backdoor=("/cmd.jsp", "/shell.jsp"),
    ),
    "dotnet": _build(
        secret=("/elmah.axd", "/trace.axd", "/appsettings.json", "/appsettings.Development.json",
                "/connectionstrings.config"),
        backdoor=("/cmd.aspx", "/shell.aspx"),
    ),
    "static": _build(info=("/_config.yml", "/config.toml", "/hugo.toml")),
}

PLATFORM_NAMES = {
    "php": "PHP", "wordpress": "WordPress", "laravel": "Laravel", "symfony": "Symfony", "drupal": "Drupal",
    "joomla": "Joomla", "magento": "Magento", "craft": "Craft CMS", "node": "Node.js", "python": "Python",
    "rails": "Ruby on Rails", "java": "Java", "dotnet": ".NET", "static": "Static site generator",
}

PHP_PLATFORMS = ("wordpress", "laravel", "symfony", "drupal", "joomla", "magento", "craft")
SCRIPT_EXTENSIONS = (".php", ".aspx", ".axd", ".jsp")
KINDS = ("secret", "info", "admin", "backdoor")
