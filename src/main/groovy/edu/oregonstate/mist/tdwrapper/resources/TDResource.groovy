package edu.oregonstate.mist.tdwrapper.resources

import com.codahale.metrics.annotation.Timed
import edu.oregonstate.mist.api.Resource
import edu.oregonstate.mist.api.jsonapi.ResourceObject
import edu.oregonstate.mist.api.jsonapi.ResultObject
import edu.oregonstate.mist.tdwrapper.db.TDServicesStaticJsonDAO
import groovy.transform.TypeChecked

import javax.annotation.security.PermitAll
import javax.ws.rs.GET
import javax.ws.rs.Path
import javax.ws.rs.PathParam
import javax.ws.rs.Produces
import javax.ws.rs.core.MediaType
import javax.ws.rs.core.Response

@Path("teamdynamix")
@Produces(MediaType.APPLICATION_JSON)
@PermitAll
@TypeChecked
class TDResource extends Resource {

    private TDServicesStaticJsonDAO tdServicesDAO

    TDResource(TDServicesStaticJsonDAO tdServicesDAO) {
        this.tdServicesDAO = tdServicesDAO
    }

    /**
     * Get all services
     * @return
     */
    @GET
    @Timed
    @Path("services")
    Response getServices() {
        ResultObject resultObject = getResultObject(tdServicesDAO.getTDServices())
        ok(resultObject).build()
    }

    /**
     * Get a service by ID
     * @param id
     * @return
     */
    @GET
    @Timed
    @Path("services/{id: [0-9a-zA-Z-]+}")
    Response getServiceByID(@PathParam("id") String id) {
        ResourceObject service = tdServicesDAO.getTDServiceByID(id)

        if (!service) {
            return notFound().build()
        }

        ResultObject resultObject = getResultObject(service)
        ok(resultObject).build()
    }

    private ResultObject getResultObject(def data) {
        new ResultObject(data: data)
    }
}
