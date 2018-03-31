/*
  Train Shape Predictor with given dataset file and images for training and testing.
  This is just a modified versuib of the example in dlib to accept more args.
*/


#include <dlib/image_processing.h>
#include <dlib/data_io.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <string.h>

using namespace dlib;
using namespace std;


std::vector<std::vector<double> > get_interocular_distances (
    const std::vector<std::vector<full_object_detection> >& objects
);

int main(int argc, char** argv)
{  
    try
    {
        if (5 > argc || 13 < argc)
        {
            cout << "Train Dlib Shape Predictor" << endl;
            cout << "Options" << endl;
            cout << "\t--trd training_dataset \t:\t XML training dataset" << endl;
            cout << "\t--tsd testing_dataset \t:\t XML testing dataset" << endl;
            cout << "\t[-o output_name] \t:\t Output model name (optional)" << endl;
            cout << "\t[--osamp oversampling] \t:\t Set Oversampling (optional)" << endl;
            cout << "\t[--nu regularization] \t:\t Set Regularization (nu) (optional)" << endl;
            cout << "\t[--tdepth tree_depth] \t:\t Set Tree Depth (optional)" << endl;
            cout << endl;
            return 0;
        }

	//datasets
	string trd, tsd, o_file;

	//prams set to default form the example 
	unsigned long oversampling = 300, tree_depth = 2;
	double nu = 0.05;


	for ( int i = 1; i < argc; i+=2)
	{
	    if(0 == strcmp("--trd", argv[i]))
	        trd = string(argv[i+1]);
	    else if (0 == strcmp("--tsd", argv[i]))
	        tsd = string(argv[i+1]);
	    else if (0 == strcmp("-o", argv[i]))
	        o_file = string(argv[i+1]);
	    else if (0 == strcmp("--osamp", argv[i]))
	        oversampling = strtoul(argv[i+1], NULL, 10);
	    else if (0 == strcmp("--nu", argv[i]))
	        nu = strtod(argv[i+1], NULL);
	    else if (0 == strcmp("--tdepth", argv[i]))
	        tree_depth = strtoul(argv[i+1], NULL, 10);
	    else { cout<<"Unknown Argument: "<<argv[i]<<endl; return 1; }
	}

        const std::string faces_directory = argv[1];
        dlib::array<array2d<unsigned char> > images_train, images_test;
        std::vector<std::vector<full_object_detection> > faces_train, faces_test;

        load_image_dataset(images_train, faces_train, trd);
        load_image_dataset(images_test, faces_test, tsd);

        // Now make the object responsible for training the model.  
        shape_predictor_trainer trainer;
        trainer.set_oversampling_amount(300);
        trainer.set_nu(0.05);
        trainer.set_tree_depth(2);


        // Tell the trainer to print status messages to the console so we can
        // see how long the training will take.
        trainer.be_verbose();

        // Now finally generate the shape model
        shape_predictor sp = trainer.train(images_train, faces_train);


        // Now that we have a model we can test it.  This function measures the
        // average distance between a face landmark output by the
        // shape_predictor and where it should be according to the truth data.
        // Note that there is an optional 4th argument that lets us rescale the
        // distances.  Here we are causing the output to scale each face's
        // distances by the interocular distance, as is customary when
        // evaluating face landmarking systems.
        cout << "mean training error: "<< 
            test_shape_predictor(sp, images_train, faces_train, get_interocular_distances(faces_train)) << endl;

        cout << "mean testing error:  "<< 
            test_shape_predictor(sp, images_test, faces_test, get_interocular_distances(faces_test)) << endl;

        // Finally, we save the model to disk so we can use it later.
        serialize(o_file) << sp;
    }
    catch (exception& e)
    {
        cout << "\nexception thrown!" << endl;
        cout << e.what() << endl;
    }
}


double interocular_distance (
    const full_object_detection& det
)
{
    dlib::vector<double,2> l, r;
    double cnt = 0;
    // Find the center of the left eye by averaging the points around 
    // the eye.
    for (unsigned long i = 36; i <= 41; ++i) 
    {
        l += det.part(i);
        ++cnt;
    }
    l /= cnt;

    // Find the center of the right eye by averaging the points around 
    // the eye.
    cnt = 0;
    for (unsigned long i = 42; i <= 47; ++i) 
    {
        r += det.part(i);
        ++cnt;
    }
    r /= cnt;

    // Now return the distance between the centers of the eyes
    return length(l-r);
}

std::vector<std::vector<double> > get_interocular_distances (
    const std::vector<std::vector<full_object_detection> >& objects
)
{
    std::vector<std::vector<double> > temp(objects.size());
    for (unsigned long i = 0; i < objects.size(); ++i)
    {
        for (unsigned long j = 0; j < objects[i].size(); ++j)
        {
            temp[i].push_back(interocular_distance(objects[i][j]));
        }
    }
    return temp;
}


