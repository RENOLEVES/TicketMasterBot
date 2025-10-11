package com.ticketmaster.repo;

import com.ticketmaster.models.Place;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

public interface PlaceRepository extends MongoRepository<Place, String> {

    List<Place> findByOfferId(String offerId);

    List<Place> findByDate(LocalDate date);

    List<Place> findByNameContaining(String name);

    @Query("{ 'offerId': ?0, 'section': ?1 }")
    List<Place> findByOfferIdAndSection(String offerId, String section);

    boolean existsByOfferId(String offerId);

    long deleteByOfferId(String offerId);
}