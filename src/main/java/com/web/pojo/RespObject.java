package com.web.pojo;

import java.util.Arrays;

public class RespObject {
    private int code;
    private String message;
    private Activity[][] activities;

    @Override
    public String toString() {
        return "RespObject{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", activities=" + Arrays.toString(activities) +
                '}';
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Activity[][] getActivities() {
        return activities;
    }

    public void setActivities(Activity[][] activities) {
        this.activities = activities;
    }
}
