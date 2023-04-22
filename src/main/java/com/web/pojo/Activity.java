package com.web.pojo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * @author Yoruko
 */
@JsonIgnoreProperties(value = {"courseId","teacherId", "roomId","taskId", "remark", "assistantName", "experiItemName", "schGroupNo", "teachClassName", "teachClassSite"})
public class Activity {
    private String teacherName;
    private String courseName;
    private String roomName;
    private String vaildWeeks;

    public Activity() {
    }

    @Override
    public String toString() {
        return "Activity{" +
                "teacherName='" + teacherName + '\'' +
                ", courseName='" + courseName + '\'' +
                ", roomName='" + roomName + '\'' +
                ", vaildWeeks='" + vaildWeeks + '\'' +
                '}';
    }

    public String getTeacherName() {
        return teacherName;
    }

    public void setTeacherName(String teacherName) {
        this.teacherName = teacherName;
    }

    public String getCourseName() {
        return courseName;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public String getRoomName() {
        return roomName;
    }

    public void setRoomName(String roomName) {
        this.roomName = roomName;
    }

    public String getVaildWeeks() {
        return vaildWeeks;
    }

    public void setVaildWeeks(String vaildWeeks) {
        this.vaildWeeks = vaildWeeks;
    }
}
