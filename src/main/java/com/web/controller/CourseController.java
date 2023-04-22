package com.web.controller;

import com.web.pojo.Activity;
import com.web.pojo.RespObject;
import com.web.service.CourseService;
import com.web.utils.RSAUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/**
 * @author Yoruko
 */
@Service
@RequestMapping("/data")
public class CourseController {
    private static final Logger logger = LoggerFactory.getLogger(CourseController.class);
    @Resource
    private CourseService courseService;

    @PostMapping("/course")
    @ResponseBody
    public RespObject getCourse(String username, String token) throws IOException, InterruptedException {
        RespObject respObject = new RespObject();
        logger.info("开始处理" + username + "的请求");
        String password;
        try{
            password = RSAUtil.decrypt(token);
        } catch (Exception e) {
            e.printStackTrace();
            logger.info("RSA解密出错");
            respObject.setCode(-1);
            respObject.setMessage("RSA解密出错");
            respObject.setActivities(null);
            return respObject;
        }
        System.setProperty("file.encoding","UTF-8");
        ProcessBuilder pb = new ProcessBuilder("python3", "login_server.py", username, password);
        Process p = pb.start();
        BufferedReader bfr = new BufferedReader(new InputStreamReader(p.getInputStream(), StandardCharsets.UTF_8));
        String line;
        while ((line = bfr.readLine()) != null) {
            System.out.println(line);
        }
        logger.info(username + "开始执行python脚本");
        p.waitFor();
        p.destroy();

        Activity[][] activities = courseService.returnJsonCourse(username);
        if(activities != null){
            respObject.setCode(1);
            respObject.setMessage("Data has been returned normally.");
            respObject.setActivities(activities);
            logger.info(username + "数据解析成功");
        }else {
            respObject.setCode(0);
            respObject.setMessage("python script run errors");
            respObject.setActivities(null);
            logger.error(username + "数据解析出错");
        }
        if(deleteFolder(new File("/cuit_agent/" + username))){
            logger.info("已删除" + username + "文件夹");
        }else {
            logger.error("删除文件" + username + "出错");
        }
        return respObject;
    }

    public static boolean deleteFolder(File folder) {
        if (folder.isDirectory()) {
            //获取该文件夹下所有的子文件夹和文件
            File[] files = folder.listFiles();
            assert files != null;
            for (File file : files) {
                //递归调用deleteFolder方法
                deleteFolder(file);
            }
        }
        //删除文件或文件夹
        return folder.delete();
    }
}
