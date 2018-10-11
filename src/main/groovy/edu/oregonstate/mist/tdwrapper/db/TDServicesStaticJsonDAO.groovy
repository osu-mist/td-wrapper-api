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
        def service = [:]
        def spanTags = [:]

        serviceRaw?.each {
            if (!(it.key in ['ID', 'Uri'])) {
                it.value = it.key.endsWith('ID') ? it.value.toString() : it.value
                service.put(it.key.uncapitalize(), it.value)
            }
        }

        serviceRaw?.SpanTagsParsedFromLongDescription?.each {
            if (it.key.startsWith('LOS')) {
                spanTags.put(it.key.replace('LOS', 'los'), it.value)
            } else if (it.key == 'SLA') {
                spanTags.put(it.key.toLowerCase(), it.value)
            } else {
                spanTags.put(it.key.uncapitalize(), it.value)
            }
        }

        service.spanTagsParsedFromLongDescription = spanTags

        new ResourceObject(
            id: serviceRaw?.ID,
            type: "service",
            attributes: service,
            links: ['self': baseUri + serviceRaw?.ID]
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
