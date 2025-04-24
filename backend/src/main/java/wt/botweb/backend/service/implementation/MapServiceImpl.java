package wt.botweb.backend.service.implementation;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.*;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import wt.botweb.backend.dto.model.map.MapDto;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Slf4j
@Service
public class MapServiceImpl implements wt.botweb.backend.service.MapService {
    private final wt.botweb.backend.repository.MapRepository mapRepository;
    private final MongoTemplate mongoTemplate;

    @Cacheable(value = "MapsCache")
    @Override
    public List<wt.botweb.backend.dto.model.map.MapDto> getMaps() {
        log.info("Retrieving all maps");
        return mapRepository.findAll()
                .stream()
                .collect(Collectors.toList());
    }

    @Cacheable(value = "MapsCache", key = "#id")
    @Override
    public wt.botweb.backend.dto.model.map.MapDto getMapsById(String id) {
        log.info("Retrieving map with ID {}", id);
        Optional<wt.botweb.backend.model.Map> map = mapRepository.findById(id);
        if (map.isPresent()) {
            return modelMapper.map(map.get(), wt.botweb.backend.dto.model.map.MapDto.class);
        }
        throw exception(entityType,exceptionType,id);
    }

    private RuntimeException exception(EntityType entityType, ExceptionType exceptionType, String... args) {
        return CCException.throwException(entityType, exceptionType, args);
    }
}
