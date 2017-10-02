package edu.oregonstate.mist.tdwrapper.db

import edu.oregonstate.mist.api.jsonapi.ResourceObject
import groovy.json.JsonSlurper

class TDServicesStaticJsonDAO {

    private File servicesFile

    TDServicesStaticJsonDAO(String sourceJsonFile) {
        servicesFile = new File(sourceJsonFile)
    }

    public List<ResourceObject> getTDServices() {
        def servicesRaw = getJsonRaw()

        List<ResourceObject> services = []

        servicesRaw.each { id, service ->
            services.add(getResourceObject(service))
        }

        services
    }

    public ResourceObject getTDServiceByID(String id) {
        def servicesRaw = getJsonRaw()

        if (!servicesRaw[id]) {
            return null
        }

        getResourceObject(servicesRaw[id])
    }

    private ResourceObject getResourceObject(def serviceRaw) {
        new ResourceObject(
                id: serviceRaw['ID'],
                type: "service",
                attributes: serviceRaw
        )
    }

    private def getJsonRaw() {
        JsonSlurper jsonSlurper = new JsonSlurper()
        jsonSlurper.parseText(servicesFile.getText())
    }
}
