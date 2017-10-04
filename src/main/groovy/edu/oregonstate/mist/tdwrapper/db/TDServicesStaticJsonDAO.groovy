package edu.oregonstate.mist.tdwrapper.db

import edu.oregonstate.mist.api.jsonapi.ResourceObject
import groovy.json.JsonSlurper

class TDServicesStaticJsonDAO {

    private File servicesFile

    TDServicesStaticJsonDAO(String sourceJsonFile) {
        servicesFile = new File(sourceJsonFile)
    }

    /**
     * Get all services
     * @return
     */
    public List<ResourceObject> getTDServices() {
        def servicesRaw = getJsonRaw()

        servicesRaw.collect { id, service -> getResourceObject(service) }
    }

    /**
     * Get service by ID
     * @param id
     * @return
     */
    public ResourceObject getTDServiceByID(String id) {
        def servicesRaw = getJsonRaw()

        if (!servicesRaw[id]) {
            return null
        }

        getResourceObject(servicesRaw[id])
    }

    /**
     * Helper method to create resource object
     * @param serviceRaw
     * @return
     */
    private ResourceObject getResourceObject(def serviceRaw) {
        new ResourceObject(
                id: serviceRaw['ID'],
                type: "service",
                attributes: serviceRaw
        )
    }

    /**
     * Helper method to slurp json file into a def
     * @return
     */
    private def getJsonRaw() {
        JsonSlurper jsonSlurper = new JsonSlurper()
        jsonSlurper.parseText(servicesFile.getText())
    }
}
