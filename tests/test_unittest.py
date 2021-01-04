import unittest
from GamepadWatchdog import compareOrders
from GamepadWatchdog import parseInputAndDevice

correctOrder=['1.2', '1.3']
correctOrderLong=['1.2', '1.3', '1.1']
correctOrderVeryLong=['1.2', '1.3', '1.0', '1.1']

class Test_compareOrders(unittest.TestCase):
	def test_same_list( self ):
		self.assertEqual( compareOrders(correctOrder, { 0: '1.2', 1 : '1.3' }), None )

	def test_same_list_wrong_key_order( self ):
		self.assertEqual( compareOrders( correctOrder, { 1: '1.3', 0 : '1.2' }), None )

	def test_wrong_order( self ):
		self.assertEqual( compareOrders( correctOrder, { 0: '1.3', 1 : '1.2' }), correctOrder )
	
	def test_correct_order_key_missed( self ):
		self.assertEqual( compareOrders( correctOrder, { 0: '1.2', 2 : '1.3' }), correctOrder )
	
	def test_correct_order_star_key_missed( self ):
		self.assertEqual( compareOrders( correctOrder, { 3: '1.2', 5 : '1.3' }), correctOrder )

	def test_wrong_order_wrong_key_order( self ):
		self.assertEqual( compareOrders( correctOrder, { 1: '1.2', 0 : '1.3' }), correctOrder )

	def test_wrong_order_key_missed( self ):
		self.assertEqual( compareOrders(correctOrder, { 2: '1.2', 0 : '1.3' }), correctOrder )

	def test_wrong_order_first_key_missed( self ):
		self.assertEqual( compareOrders( correctOrder, { 3: '1.2', 1 : '1.3' }), correctOrder )

	def test_different_set_ports( self ):
		self.assertEqual( compareOrders( correctOrder, { 0: '1.2', 1 : '1.4' }), None )

	def test_different_set_lower_amount_of_ports( self ):
		self.assertEqual( compareOrders( correctOrderLong, { 0: '1.2', 2 : '1.3' }), correctOrder)

	def test_different_set_ports_not_reordable( self ):
		self.assertEqual( compareOrders( correctOrder, { 0: '1.2', 1 : '1.4', 2 : '1.5' }), None )

	def test_different_set_ports_but_reordable( self ):
		self.assertEqual( compareOrders( correctOrder, { 0: '1.2', 1 : '1.4', 2 : '1.3' }), [ '1.2', '1.3', '1.4'] )
	
	def test_more_than_needed_reorder_not_required( self ):
		self.assertEqual( compareOrders( correctOrder, { 0: '1.2', 1 : '1.3', 2 : '1.4' }), None )
	
	def test_more_than_needed_reorder_is_required( self ):
		self.assertEqual( compareOrders( correctOrder, { 1: '1.2', 0 : '1.3', 2 : '1.4' }), [ '1.2', '1.3', '1.4'] )

	def test_more_than_needed_reorder_is_required_2( self ):
		self.assertEqual( compareOrders( correctOrder, { 0: '1.2', 2 : '1.3', 1 : '1.4' }), [ '1.2', '1.3', '1.4'] )
	
	def test_one_gamepad_port_1( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 0: '1.2'}), None )
	
	def test_one_gamepad_port_2( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 0: '1.3'}), None )
	
	def test_one_gamepad_left_port_2( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 1: '1.3'}), None )

	def test_two_gamepad_misordered( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 1: '1.2', 0: '1.3' }), correctOrder )
	
	def test_two_gamepad_ordered( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 1: '1.3', 0: '1.2' }), None )
	
	def test_one_first_gamepad_ordered( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 0: '1.2' }), None )
	
	def test_one_first_gamepad_misordered( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 1: '1.2' }), ['1.2'] )

	def test_one_second_gamepad_ordered( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 1: '1.3' }), None )
	
	def test_one_second_gamepad_misordered( self ):
		self.assertEqual( compareOrders( correctOrderVeryLong, { 0: '1.3' }), None )

class Test_parseInputAndDevice(unittest.TestCase):
	def test_event_joystick_match( self ):
		self.assertEqual( parseInputAndDevice( 'platform-3f980000.usb-usb-0:1.2:1.0-event-joystick../event0'), [0, '1.2'] )
	def test_event_not_joystick_match( self ):
		self.assertEqual( parseInputAndDevice( 'platform-3f980000.usb-usb-0:1.2:1.0-event-keyboard../event0'), [0, '1.2'] )
	def test_not_event_joystick_match( self ):
		self.assertEqual( parseInputAndDevice( 'platform-3f980000.usb-usb-0:1.2:1.0-joystick../js0'), None )

if __name__ == "__main__":
	unittest.main()
