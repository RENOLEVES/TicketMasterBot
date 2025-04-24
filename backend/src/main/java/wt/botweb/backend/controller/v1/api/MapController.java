package wt.botweb.backend.controller.v1.api;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import wt.botweb.backend.dto.response.Response;
import wt.botweb.backend.service.MapService;
import wt.botweb.backend.service.implementation.MapServiceImpl;

import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/seatMap")
public class MapController {

    private final MapServiceImpl mapService;
    @GetMapping
    public Response<?> getMaps() {
        return Response
                .ok()
                .setPayload(mapService.getMaps());
    }

    @GetMapping("/{artist_name}={id}")
    public Response<?> getMapById(@PathVariable String id, @RequestParam(???)) {
        Object map = mapService.getMapsById(id);
        return Response.ok().setPayload(map);
    }
}
