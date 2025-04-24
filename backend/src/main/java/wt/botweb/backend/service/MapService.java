package wt.botweb.backend.service;

import wt.botweb.backend.dto.model.map.MapDto;

import java.util.List;

public interface MapService {
    List<MapDto> getMaps();
    MapDto getMapsById(String id);
}
