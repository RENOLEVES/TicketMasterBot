package wt.botweb.backend.service.implementation;

import com.google.gson.reflect.TypeToken;
import wt.botweb.backend.model.Map;
import wt.botweb.backend.service.SeedService;
import wt.botweb.backend.util.JsonUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;
import java.util.List;

@Service
@Slf4j
public class SeedServiceImpl implements SeedService<Map> {
    @Override
    public List<Map> readSeedFromFile(Path path) {

        if (Files.notExists(path)) {
            log.error("Seed file does not exist at path: {}", path);
            return Collections.emptyList();
        }
        List<Map> data = JsonUtils.getData(path, new TypeToken<List<Map>>(){});

        return data == null ? Collections.emptyList() : data;
    }
}
