from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

CUPCAKE_DATA_3 = {
    "flavor": "TestFlavor3",
    "size": "TestSize3",
    "rating": 3,
    "image": "http://test.com/cupcake3.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """ Check that all data on all cupcakes show
            Expected Result: {"cupcakes": [
                    {
                "flavor": "Vanilla Test",
                "id": 6,
                "image": "http://test.com/cupcake.jpg",
                "rating": 5,
                "size": "TestSize"
                    }
            ]}"""

        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json.copy()

            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        """ Check that individual cupcake is shown in cupcakes database """

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """ Check that new cupcake is added to cupcakes database """

        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json.copy()

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_patch_cupcake(self):
        """ Check that cupcake is edited and the updates on cupcakes
            appear in cupcakes database
        """

        with app.test_client() as client:

            # Make a get request to get cupcake instance with cupcake.id
            url = f"/api/cupcakes/{self.cupcake.id}"
            # resp = client.post(url, json=CUPCAKE_DATA_3)

            # cupcake_to_patch = resp.json.copy()
            updated_cupcake = {"cupcake": CUPCAKE_DATA}
            updated_cupcake["cupcake"]["flavor"] = "Vanilla Test"

            # resp = client.patch(url, json=updated_cupcake)
            resp = client.patch(url, json={"cupcake": {"flavor": "CHOCOLATE"}})

            data = resp.get_json()

            # test for proper response code
            self.assertEqual(resp.status_code, 200)

            # self.assertEqual(data["cupcake"]["flavor"], "Vanilla Test")
            self.assertEqual(data["cupcake"], {
                "flavor": "CHOCOLATE",
                "id": self.cupcake.id,
                "size": "TestSize",
                "rating": 5,
                "image": "http://test.com/cupcake.jpg"
            })

    def test_delete_cupcakes(self):
        """ Check that selected cupcake is deleted and does not
            appear in cupcakes database
        """

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            # resp_cupcakes = client.get()
            # print(resp_cupcakes, "<------------------resp cupcakes")

            # breakpoint()
            # data = resp_cupcakes.get_json()
            # print(data, "<-----------------------------------data")

            data = resp.json

            self.assertEqual(resp.status_code, 200)
            self.assertEqual({'deleted': self.cupcake.id},
                             data)
# #             CUPCAKE_DATA = {
#               "flavor": "TestFlavor",
#               "size": "TestSize",
#               "rating": 5,
#               "image": "http://test.com/cupcake.jpg"
# }

            #  self.assertEqual(data["cupcake"] {
            # "flavor": "Vanilla Test",
            # "id": self.cupcake.id,
            # "size": "TestSize",
            # "rating": 5,
            # "image": "http://test.com/cupcake.jpg"
            # }
