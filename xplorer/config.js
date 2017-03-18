var config = {}

config.host = process.env.HOST || "https://vplusplus.documents.azure.com:443/";
config.authKey = process.env.AUTH_KEY || "aLSJt0fu1cGEpFNvOQtBgbaZ4if7SfwEpka4Co29WLS74KRunJLkUTcTAPHEHMUxbS6iHW7MfyNHTmf4EPGk7w==";
config.databaseId = "ToDoList";
config.collectionId = "Items";

module.exports = config;