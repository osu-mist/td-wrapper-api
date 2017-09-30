package edu.oregonstate.mist.tdwrapper.db

import edu.oregonstate.mist.api.jsonapi.ResourceObject
import groovy.json.JsonSlurper

class TDServicesStaticJsonDAO {

    private File servicesFile
    private JsonSlurper jsonSlurper = new JsonSlurper()

    TDServicesStaticJsonDAO(String sourceJsonFile) {
        servicesFile = new File(sourceJsonFile)
    }

    public List<ResourceObject> getTDServices() {
        def servicesRaw = jsonSlurper.parseText(servicesFile.getText())

        List<ResourceObject> services = []

        servicesRaw.each { id, service ->
            services.add(getResourceObject(service))
        }

        services
    }

    private ResourceObject getResourceObject(def serviceRaw) {
        new ResourceObject(
                id: serviceRaw['ID'],
                type: "service",
                attributes: serviceRaw
        )
    }
}
