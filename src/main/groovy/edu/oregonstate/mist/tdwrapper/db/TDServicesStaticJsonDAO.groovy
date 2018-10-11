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
    public List<ResourceObject> getTDServices(String baseUri) {
        def servicesRaw = getJsonRaw()
        servicesRaw.collect { id, service -> getResourceObject(service, baseUri) }
    }

    /**
     * Get service by ID
     * @param id
     * @return
     */
    public ResourceObject getTDServiceByID(String id, String baseUri) {
        def servicesRaw = getJsonRaw()

        if (!servicesRaw[id]) {
            return null
        }

        getResourceObject(servicesRaw[id], baseUri)
    }

    /**
     * Helper method to create resource object
     * @param serviceRaw
     * @return
     */
    private ResourceObject getResourceObject(def serviceRaw, String baseUri) {
        def serviceID = serviceRaw?.ID
        def service = [:]

        ['ID', 'Uri'].each { serviceRaw.remove(it) }
        serviceRaw?.each {
            if (it.key.endsWith('ID')) {
                it.value = it.value.toString()
            }

            service.put(it.key.uncapitalize(), it.value)
            service.remove(it.key)
        }

        new ResourceObject(
            id: serviceID,
            type: "service",
            attributes: service,
            links: ['self': baseUri + serviceID]
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
