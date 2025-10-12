package com.ticketmaster.controllers;

import com.ticketmaster.models.*;
import com.ticketmaster.repo.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/query")
public class QueryController {

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

    @GetMapping("/places")
    public List<Place> getAllPlaces() {
        return placeRepository.findAll();
    }

    @GetMapping("/prices")
    public List<Price> getAllPrices() {
        return priceRepository.findAll();
    }

    @GetMapping("/ranges")
    public List<OfferRange> getAllRanges() {
        return offerRangeRepository.findAll();
    }

    @GetMapping("/seats")
    public List<Seat> getAllSeats() {
        return seatRepository.findAll();
    }

    @GetMapping("/results")
    public List<Result> getAllResults() {
        return resultRepository.findAll();
    }

    @GetMapping("/count")
    public String getCounts() {
        return String.format(
                "数据统计: Places: %d, Prices: %d, Ranges: %d, Seats: %d, Results: %d",
                placeRepository.count(),
                priceRepository.count(),
                offerRangeRepository.count(),
                seatRepository.count(),
                resultRepository.count()
        );
    }
}