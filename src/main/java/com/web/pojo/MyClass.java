package com.web.pojo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.Arrays;

/**
 * @author Yoruko
 */
@JsonIgnoreProperties(value = {"unitCounts", "year", "endAtSat", "marshalContents"})
public class MyClass{
    private Activity[][] activities;
    public MyClass() {
    }

    @Override
    public String toString() {
        return "MyClass{" +
                "activities=" + Arrays.toString(activities) +
                '}';
    }

    public Activity[][] getActivities() {
        return activities;
    }

    public void setActivities(Activity[][] activities) {
        this.activities = activities;
    }
}
