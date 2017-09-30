package edu.oregonstate.mist.tdwrapper.resources

import com.codahale.metrics.annotation.Timed
import edu.oregonstate.mist.api.Resource
import edu.oregonstate.mist.api.jsonapi.ResultObject
import edu.oregonstate.mist.tdwrapper.db.TDServicesStaticJsonDAO
import groovy.transform.TypeChecked

import javax.annotation.security.PermitAll
import javax.ws.rs.GET
import javax.ws.rs.Path
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

    @GET
    @Timed
    @Path("services")
    Response getServices() {
        ResultObject resultObject = new ResultObject(
                data: tdServicesDAO.getTDServices()
        )

        ok(resultObject).build()
    }
}
