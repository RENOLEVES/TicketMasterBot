package com.ticketmaster.controllers;

import com.ticketmaster.services.DataInitService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/data")
public class DataController {

    @Autowired
    private DataInitService dataInitService;

    @GetMapping("/init-data")
    public String initializeData() {
        try {
            dataInitService.initializeSampleData();
            return "Data has been initialized,";
        } catch (Exception e) {
            return "Data initialization failed: " + e.getMessage();
        }
    }
    @PostMapping("/init-data")
    public String initializeDataPost() {
        return initializeData();
    }

    @PostMapping("/init/{tableName}")
    public String initializeTable(@PathVariable String tableName) {
        try {
            dataInitService.initializeSampleData();
            return "Table " + tableName + " initialized successfully！";
        } catch (Exception e) {
            return "Table " + tableName + " failed to initialize: " + e.getMessage();
        }
    }
}