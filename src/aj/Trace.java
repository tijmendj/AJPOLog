package aj;

import java.lang.reflect.Field;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.JoinPoint.StaticPart;

class Trace {
	public static final Logger logger = LogManager.getLogger("AJPOLog");

	public static boolean doesObjectContainField(Object object, String fieldName) {
		Class<?> objectClass = object.getClass();
		for (Field field : objectClass.getFields()) {
			if (field.getName().equals(fieldName)) {
				return true;
			}
		}
		return false;
	}

	public static void logMethodCall(String entry, JoinPoint joinpoint, StaticPart enclosingJoinPoint,
			Object targetObject, StaticPart jpsp) {
		// Enclosing JoinPoint
		// The enclosing JoinPoint of a *call* is the caller. This is not the case for
		// an execution. The long string will say execution if though we use a call
		// JoinPoint
		String message = jpsp.getSignature().toLongString();

		Object joinPointThis = joinpoint.getThis();

		String callerId = getId(joinPointThis);
		String calleeId = getId(targetObject);

		// Get caller and callee full string representation
		String callerName = String.format("%s.%s", enclosingJoinPoint.getSignature().getDeclaringTypeName(), callerId);
		String calleeName = String.format("%s.%s", targetObject.getClass().getCanonicalName(), calleeId);

		logger.trace(String.format("%s;%s;%s;%s", entry, callerName, calleeName, message));
	}

	private static String getId(Object subject) {
		// "Returns null when there is no currently executing object available.
		// This includes all join points that occur in a static context."
		int psuedoId = 0;
		boolean psuedoIdIsSet = false;

		if (subject != null) {
			psuedoId = System.identityHashCode(subject);
			psuedoIdIsSet = true;
		}

		String id = "Static";
		if (psuedoIdIsSet) {
			id = "CallerPsuedoId: " + psuedoId;
		}

		return id;
	}
}
