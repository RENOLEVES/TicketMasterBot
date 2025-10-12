package com.ticketmaster.services;

import com.ticketmaster.models.*;
import com.ticketmaster.repo.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

@Service
public class DataInitService {

    @Autowired
    private PlaceRepository placeRepository;

    @Autowired
    private PriceRepository priceRepository;

    @Autowired
    private OfferRangeRepository offerRangeRepository;

    @Autowired
    private SeatRepository seatRepository;

    @Autowired
    private ResultRepository resultRepository;

    public void initializeSampleData() {
        // 清理现有数据
        placeRepository.deleteAll();
        priceRepository.deleteAll();
        offerRangeRepository.deleteAll();
        seatRepository.deleteAll();
        resultRepository.deleteAll();

        System.out.println("开始初始化示例数据...");

        // 1. 初始化 PLACE 表数据
        initializePlaces();

        // 2. 初始化 PRICE 表数据
        initializePrices();

        // 3. 初始化 RANGE 表数据
        initializeRanges();

        // 4. 初始化 SEAT 表数据
        initializeSeats();

        // 5. 初始化 RESULT 表数据
        initializeResults();

        System.out.println("sample initialized！");
    }

    private void initializePlaces() {
        List<Place> places = Arrays.asList(
                createPlace("Taylor Swift Concert", "2024-12-15", "VIP", "Madison Square Garden", "TSWIFT001"),
                createPlace("Coldplay Tour", "2024-11-20", "A", "Staples Center", "COLDPLAY001"),
                createPlace("NBA Finals", "2024-06-10", "Lower Bowl", "Chase Center", "NBA001"),
                createPlace("Broadway Show", "2024-09-05", "Orchestra", "Broadway Theater", "BROADWAY001"),
                createPlace("Comedy Night", "2024-08-12", "General", "Comedy Club", "COMEDY001")
        );

        placeRepository.saveAll(places);
        System.out.println("PLACE initialized: " + places.size() + " records");
    }

    private void initializePrices() {
        List<Price> prices = Arrays.asList(
                createPrice("Taylor Swift Concert", "2024-12-15", "TSWIFT001", "VIP", new BigDecimal("499.99")),
                createPrice("Taylor Swift Concert", "2024-12-15", "TSWIFT001", "Standard", new BigDecimal("199.99")),
                createPrice("Coldplay Tour", "2024-11-20", "COLDPLAY001", "Premium", new BigDecimal("299.99")),
                createPrice("NBA Finals", "2024-06-10", "NBA001", "Courtside", new BigDecimal("1500.00")),
                createPrice("Broadway Show", "2024-09-05", "BROADWAY001", "Orchestra", new BigDecimal("189.50"))
        );

        priceRepository.saveAll(prices);
        System.out.println("PRICE initialized: " + prices.size() + " records");
    }

    private void initializeRanges() {
        List<OfferRange> ranges = Arrays.asList(
                createRange("Taylor Swift Concert", "2024-12-15", "TSWIFT001", "VIP Packages Only"),
                createRange("Coldplay Tour", "2024-11-20", "COLDPLAY001", "North America Tour"),
                createRange("NBA Finals", "2024-06-10", "NBA001", "Championship Series"),
                createRange("Broadway Show", "2024-09-05", "BROADWAY001", "Limited Engagement"),
                createRange("Comedy Night", "2024-08-12", "COMEDY001", "Weekend Special")
        );

        offerRangeRepository.saveAll(ranges);
        System.out.println("RANGE initialized: " + ranges.size() + " records");
    }

    private void initializeSeats() {
        List<Seat> seats = Arrays.asList(
                createSeat("Taylor Swift Concert", "2024-12-15", new BigDecimal("499.99"), "Front Row VIP", "VIP", "1", "VIP", "TSWIFT001", Seat.SeatStatus.AVAILABLE),
                createSeat("Taylor Swift Concert", "2024-12-15", new BigDecimal("199.99"), "Standard View", "A", "10", "Standard", "TSWIFT001", Seat.SeatStatus.AVAILABLE),
                createSeat("Coldplay Tour", "2024-11-20", new BigDecimal("299.99"), "Premium Sound", "B", "5", "Premium", "COLDPLAY001", Seat.SeatStatus.RESERVED),
                createSeat("NBA Finals", "2024-06-10", new BigDecimal("1500.00"), "Courtside Experience", "Courtside", "2", "Elite", "NBA001", Seat.SeatStatus.AVAILABLE),
                createSeat("Broadway Show", "2024-09-05", new BigDecimal("189.50"), "Orchestra Center", "Orchestra", "8", "Premium", "BROADWAY001", Seat.SeatStatus.SOLD)
        );

        seatRepository.saveAll(seats);
        System.out.println("SEAT initialized: " + seats.size() + " records");
    }

    private void initializeResults() {
        List<Result> results = Arrays.asList(
                createResult(new BigDecimal("449.99"), "Best Available Price", "VIP", "TSWIFT001", "Price Calculation", Result.ResultStatus.SUCCESS),
                createResult(new BigDecimal("279.99"), "Average Price", "Premium", "COLDPLAY001", "Market Analysis", Result.ResultStatus.SUCCESS),
                createResult(new BigDecimal("1200.00"), "Premium Seating", "Elite", "NBA001", "Revenue Forecast", Result.ResultStatus.PENDING),
                createResult(new BigDecimal("175.00"), "Standard Pricing", "Standard", "BROADWAY001", "Competitive Analysis", Result.ResultStatus.SUCCESS)
        );

        resultRepository.saveAll(results);
        System.out.println("RESULT initialized: " + results.size() + " records");
    }

    // 辅助方法
    private Place createPlace(String name, String date, String section, String place, String offerId) {
        Place p = new Place();
        p.setName(name);
        p.setDate(LocalDate.parse(date));
        p.setSection(section);
        p.setPlace(place);
        p.setOfferId(offerId);
        return p;
    }

    private Price createPrice(String name, String date, String offerId, String branding, BigDecimal totalPrice) {
        Price p = new Price();
        p.setName(name);
        p.setDate(LocalDate.parse(date));
        p.setOfferId(offerId);
        p.setBranding(branding);
        p.setTotalPrice(totalPrice);
        return p;
    }

    private OfferRange createRange(String name, String date, String offerId, String offerRange) {
        OfferRange r = new OfferRange();
        r.setName(name);
        r.setDate(LocalDate.parse(date));
        r.setOfferId(offerId);
        r.setOfferRange(offerRange);
        return r;
    }

    private Seat createSeat(String name, String date, BigDecimal price, String description,
                            String section, String row, String branding, String offerId, Seat.SeatStatus status) {
        Seat s = new Seat();
        s.setName(name);
        s.setDate(LocalDate.parse(date));
        s.setPrice(price);
        s.setDescription(description);
        s.setSection(section);
        s.setRow(row);
        s.setBranding(branding);
        s.setOfferId(offerId);
        s.setStatus(status);
        return s;
    }

    private Result createResult(BigDecimal price, String description, String branding,
                                String offerId, String resultType, Result.ResultStatus status) {
        Result r = new Result();
        r.setPrice(price);
        r.setDescription(description);
        r.setBranding(branding);
        r.setOfferId(offerId);
        r.setResultType(resultType);
        r.setStatus(status);
        return r;
    }
}