package edu.oregonstate.mist.tdwrapper

import edu.oregonstate.mist.api.Application
import edu.oregonstate.mist.api.Configuration
import edu.oregonstate.mist.tdwrapper.db.TDServicesStaticJsonDAO
import edu.oregonstate.mist.tdwrapper.resources.TDResource
import io.dropwizard.setup.Environment

/**
 * Main application class.
 */
class TDWrapperApplication extends Application<TDWrapperConfiguration> {
    /**
     * Parses command-line arguments and runs the application.
     *
     * @param configuration
     * @param environment
     */
    @Override
    public void run(TDWrapperConfiguration configuration, Environment environment) {
        this.setup(configuration, environment)

        final TDServicesStaticJsonDAO TDSERVICESDAO = new TDServicesStaticJsonDAO(
                configuration.tdServicesJson)
        environment.jersey().register(new TDResource(TDSERVICESDAO))
    }

    /**
     * Instantiates the application class with command-line arguments.
     *
     * @param arguments
     * @throws Exception
     */
    public static void main(String[] arguments) throws Exception {
        new TDWrapperApplication().run(arguments)
    }
}
