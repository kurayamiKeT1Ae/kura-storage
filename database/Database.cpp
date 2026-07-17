#include "Database.h"
#include <Arduino.h>
#include <ArduinoJson.h>
#include <LittleFS.h>

Database::Database(const char* filename){
  path = filename;
}

void Database::load(){
  File file = LittleFS.open(path, "r");
  deserializeJson(data, file);
  file.close();
}

void Database::save(){
  File file = LittleFS.open(path, "w");
  serializeJson(data, file);
  file.close();
}

void Database::add(const char *website, const char *name,const char *password){
  data[website]["username"] = name;
  data[website]["password"] = password;

  save();
}

void Database::edit(const char *oldWebsite, const char *website, const char *name, const char *password){
  if (strcmp(oldWebsite, website) != 0 ){
    data[website]["username"] = name;
    data[website]["password"] = password;

    data.remove(oldWebsite);
  } else {
    data[oldWebsite]["username"] = name;
    data[oldWebsite]["password"] = password;
  }

  save();
}

JsonObject Database::get(const char* website){
  return data[website].as<JsonObject>();
}

void Database::del(const char* website){
  data.remove(website);
  save();
}

