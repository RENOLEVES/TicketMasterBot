package com.ticketmaster.repo;

import com.ticketmaster.models.Seat;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import java.time.LocalDate;
import java.math.BigDecimal;
import java.util.List;

public interface SeatRepository extends MongoRepository<Seat, String> {

    List<Seat> findByOfferId(String offerId);

    List<Seat> findBySectionAndRow(String section, String row);

    List<Seat> findByStatus(Seat.SeatStatus status);

    List<Seat> findByDateAndSection(LocalDate date, String section);

    @Query("{ 'offer_id': ?0, 'price': { $lte: ?1 } }")
    List<Seat> findByOfferIdAndPriceLessThanEqual(String offerId, BigDecimal maxPrice);

    @Query("{ 'section': ?0, 'status': 'AVAILABLE' }")
    List<Seat> findAvailableSeatsBySection(String section);

    @Query("{ 'offer_id': ?0, 'status': 'AVAILABLE' }")
    List<Seat> findAvailableSeatsByOfferId(String offerId);

    @Query(value = "{ 'offer_id': ?0 }", count = true)
    long countByOfferId(String offerId);

    @Query(value = "{ 'offer_id': ?0, 'status': ?1 }", count = true)
    long countByOfferIdAndStatus(String offerId, Seat.SeatStatus status);
}