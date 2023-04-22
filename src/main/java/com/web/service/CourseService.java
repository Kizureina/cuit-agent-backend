package com.web.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.web.pojo.Activity;
import com.web.pojo.MyClass;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

/**
 * @author Yoruko
 */
@Service
public class CourseService {
    private static final Logger logger = LoggerFactory.getLogger(CourseService.class);

    public Activity[][] returnJsonCourse(String username) {
        logger.info(username + "开始读取json文件");
        String path = "/cuit_agent/" + username;
        File file = new File(path);
        if(!file.isDirectory()){
            logger.error(username + "文件不存在");
            return null;
        }
        File[] files = file.listFiles();
        File jsonFile = null;
        if(files != null){
            jsonFile = files[0];
        }
        ObjectMapper objectMapper = new ObjectMapper();

        try {
            MyClass myClass = objectMapper.readValue(getStr(jsonFile), MyClass.class);
            logger.info("读取" + username + "json文件完成");
            return myClass.getActivities();
//            for (Activity[] activity : activities) {
//                for (Activity activity1 : activity) {
//                    System.out.println(activity1);
//                }
//            }
//            for (int i = 0; i < activities.length; i++) {
//                System.out.println("第" + i + "节课");
//                try{
//                    System.out.println(activities[i][0]);
//                }catch(Exception e){
//                    System.out.println(0);
//                }
//            }
        } catch (IOException e) {
            logger.error("读取" + username + "json文件失败");
            e.printStackTrace();
        }

        return null;
    }

    public static String getStr(File jsonFile){
        String jsonStr;
        try {
            FileReader fileReader = new FileReader(jsonFile);
            Reader reader = new InputStreamReader(Files.newInputStream(jsonFile.toPath()), StandardCharsets.UTF_8);
            int ch;
            StringBuilder sb = new StringBuilder();
            while ((ch = reader.read()) != -1) {
                sb.append((char) ch);
            }
            fileReader.close();
            reader.close();
            jsonStr = sb.toString();
            return jsonStr;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
